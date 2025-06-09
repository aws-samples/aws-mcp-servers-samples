"""Session management for MCP server using DynamoDB"""
import uuid
import time
from typing import Optional, Dict, Any
import boto3
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages MCP sessions using DynamoDB"""
    
    def __init__(self, table_name: str = "mcp_sessions"):
        """Initialize the session manager
        
        Args:
            table_name: Name of DynamoDB table to use for sessions
        """
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
        
    @classmethod
    def create_table(cls, table_name: str = "mcp_sessions") -> None:
        """Create the DynamoDB table for sessions if it doesn't exist
        
        Args:
            table_name: Name of the table to create
        """
        dynamodb = boto3.resource('dynamodb')
        
        try:
            # Check if table exists
            dynamodb.Table(table_name).table_status
            logger.info(f"Table {table_name} already exists")
            return
        except:
            # Create table if it doesn't exist
            table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'session_id',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'session_id',
                        'AttributeType': 'S'
                    }
                ],
                BillingMode='PAY_PER_REQUEST',
                TimeToLiveSpecification={
                    'Enabled': True,
                    'AttributeName': 'expires_at'
                }
            )
            
            # Wait for table to be created
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            logger.info(f"Created table {table_name}")
    
    def create_session(self, session_data: Optional[Dict[str, Any]] = None) -> str:
        """Create a new session
        
        Args:
            session_data: Optional initial session data
            
        Returns:
            The session ID
        """
        # Generate a secure random UUID for the session
        session_id = str(uuid.uuid4())
        
        # Set session expiry to 24 hours from now
        expires_at = int(time.time()) + (24 * 60 * 60)
        
        # Store session in DynamoDB
        item = {
            'session_id': session_id,
            'expires_at': expires_at,
            'created_at': int(time.time()),
            'data': session_data or {}
        }
        
        self.table.put_item(Item=item)
        logger.info(f"Created session {session_id}")
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data
        
        Args:
            session_id: The session ID to look up
            
        Returns:
            Session data or None if not found
        """
        try:
            response = self.table.get_item(Key={'session_id': session_id})
            item = response.get('Item')
            
            if not item:
                return None
                
            # Check if session has expired
            if item.get('expires_at', 0) < time.time():
                self.delete_session(session_id)
                return None
                
            return item.get('data', {})
            
        except Exception as e:
            logger.error(f"Error getting session {session_id}: {e}")
            return None
    
    def update_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Update session data
        
        Args:
            session_id: The session ID to update
            session_data: New session data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.table.update_item(
                Key={'session_id': session_id},
                UpdateExpression='SET #data = :data',
                ExpressionAttributeNames={'#data': 'data'},
                ExpressionAttributeValues={':data': session_data}
            )
            return True
        except Exception as e:
            logger.error(f"Error updating session {session_id}: {e}")
            return False
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session
        
        Args:
            session_id: The session ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.table.delete_item(Key={'session_id': session_id})
            logger.info(f"Deleted session {session_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {e}")
            return False 