#!/usr/bin/env python3
"""
文档摄取脚本：读取文本文件，拆分为chunks，转换为向量并存储到OpenSearch
只用于文档摄入aos，不用于MCP
"""

import os
import sys
import argparse
import logging
import asyncio
from typing import List, Dict, Optional, Any
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.text_splitter import RecursiveCharacterTextSplitter
from aos_client import OpenSearchClient
from tools.embedding import EmbeddingTools

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("doc_ingest")

class DocumentIngestor:
    """文档摄取器：处理文档并将其存储到OpenSearch"""
    
    def __init__(
        self, 
        opensearch_host: str,
        opensearch_port: int,
        index_name: str,
        username: str = None,
        password: str = None,
        embedding_api_token: str = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        初始化文档摄取器
        
        Args:
            opensearch_host: OpenSearch主机地址
            opensearch_port: OpenSearch端口
            index_name: 索引名称
            username: OpenSearch用户名
            password: OpenSearch密码
            embedding_api_token: 嵌入API令牌
            chunk_size: 文本块大小
            chunk_overlap: 文本块重叠大小
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # 初始化OpenSearch客户端
        self.aos_client = OpenSearchClient(
            opensearch_host=opensearch_host,
            opensearch_port=opensearch_port,
            index_name=index_name,
            username=username,
            password=password,
            use_ssl=True,
            verify_certs=True,
            ssl_assert_hostname=False,
            ssl_show_warn=True
        )
        
        # 初始化嵌入工具
        self.embedding_tools = EmbeddingTools(
            aos_client=self.aos_client,
            api_token=embedding_api_token
        )
        
        # 初始化文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", "。", "，", " ", ""]
        )
        
        logger.info(f"初始化文档摄取器，索引: {index_name}, 块大小: {chunk_size}, 块重叠: {chunk_overlap}")

    async def create_index_if_not_exists(self) -> None:
        """创建索引（如果不存在）"""
        client = self.aos_client.get_client()

        # 检查索引是否存在
        index_exists = client.indices.exists(index=self.aos_client._index_name)
        if not index_exists:
            # 创建索引并设置映射
            mapping = {
                "settings": {
                    "index": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0,
                        "refresh_interval": "60s",
                        "knn": True,
                        "knn.algo_param.ef_search": 32
                    }
                },
                "mappings": {
                    "properties": {
                        "dense_vector": {
                            "type": "knn_vector",
                            "dimension": 1024,
                            "method": {
                                "name": "hnsw",
                                "space_type": "innerproduct",
                                "engine": "faiss",
                                "parameters": {
                                    "ef_construction": 32,
                                    "m": 16
                                }
                            }
                        },
                        "text": {"type": "text"},
                        "metadata": {"type": "object"}
                    }
                }
            }

            client.indices.create(
                index=self.aos_client._index_name,
                body=mapping
            )
            logger.info(f"创建索引 {self.aos_client._index_name} 及映射")
        else:
            logger.info(f"索引 {self.aos_client._index_name} 已存在")
    
    def read_text_file(self, file_path: str) -> str:
        """
        读取文本文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件内容
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            logger.info(f"读取文件 {file_path}，大小: {len(content)} 字符")
            return content
        except Exception as e:
            logger.error(f"读取文件 {file_path} 失败: {str(e)}")
            raise
    
    def split_text(self, text: str) -> List[str]:
        """
        将文本拆分为块
        
        Args:
            text: 要拆分的文本
            
        Returns:
            文本块列表
        """
        chunks = self.text_splitter.split_text(text)
        logger.info(f"文本拆分为 {len(chunks)} 个块")
        return chunks
    
    async def process_file(self, file_path: str, metadata: Dict = None) -> Dict:
        """
        处理文件：读取、拆分、嵌入和索引
        
        Args:
            file_path: 文件路径
            metadata: 可选的元数据
            
        Returns:
            处理结果
        """
        try:
            # 确保索引存在
            await self.create_index_if_not_exists()
            
            # 读取文件
            text = self.read_text_file(file_path)
            
            # 拆分文本
            chunks = self.split_text(text)
            
            # 准备文档列表
            documents = []
            base_metadata = metadata or {}
            base_metadata["source"] = file_path
            base_metadata["filename"] = os.path.basename(file_path)
            
            for i, chunk in enumerate(chunks):
                # 为每个块创建文档
                doc = {
                    "text": chunk,
                    "metadata": {
                        **base_metadata,
                        "chunk_index": i,
                        "chunk_count": len(chunks)
                    }
                }
                documents.append(doc)
            
            # 批量索引文档
            result = await self.embedding_tools.bulk_index_with_embeddings(documents)
            
            if result["status"] == "success":
                logger.info(f"成功索引 {result['processed_count']} 个文档块")
            else:
                logger.error(f"索引文档失败: {result['message']}")
            
            return result
            
        except Exception as e:
            logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
            return {"status": "error", "message": str(e)}

async def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="文档摄取脚本")
    parser.add_argument("--file", required=True, help="要处理的文件路径")
    parser.add_argument("--host", default=os.environ.get("OPENSEARCH_HOST", ""), help="OpenSearch主机")
    parser.add_argument("--port", type=int, default=int(os.environ.get("OPENSEARCH_PORT", "443")), help="OpenSearch端口")
    parser.add_argument("--index", default=os.environ.get("OPENSEARCH_INDEX", "dockb-index"), help="OpenSearch索引名称")
    parser.add_argument("--username", default=os.environ.get("OPENSEARCH_USERNAME", ""), help="OpenSearch用户名")
    parser.add_argument("--password", default=os.environ.get("OPENSEARCH_PASSWORD", ""), help="OpenSearch密码")
    parser.add_argument("--token", default=os.environ.get("EMBEDDING_API_TOKEN", ""), help="嵌入API令牌")
    parser.add_argument("--chunk-size", type=int, default=1000, help="文本块大小")
    parser.add_argument("--chunk-overlap", type=int, default=200, help="文本块重叠大小")
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.isfile(args.file):
        logger.error(f"文件不存在: {args.file}")
        sys.exit(1)
    
    # 初始化文档摄取器
    ingestor = DocumentIngestor(
        opensearch_host=args.host,
        opensearch_port=args.port,
        index_name=args.index,
        username=args.username,
        password=args.password,
        embedding_api_token=args.token,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap
    )
    
    # 处理文件
    result = await ingestor.process_file(args.file)
    
    # 输出结果
    if result["status"] == "success":
        logger.info("文档处理成功")
        sys.exit(0)
    else:
        logger.error(f"文档处理失败: {result['message']}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
