"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AosPublicSetupStack = void 0;
const cdk = require("aws-cdk-lib");
const opensearch = require("aws-cdk-lib/aws-opensearchservice");
const ec2 = require("aws-cdk-lib/aws-ec2");
const iam = require("aws-cdk-lib/aws-iam");
const fs = require("fs");
const path = require("path");
class AosPublicSetupStack extends cdk.Stack {
    constructor(scope, id, props) {
        super(scope, id, props);
        // 创建OpenSearch域 - 使用公共访问模式（不在VPC内）
        const domain = new opensearch.Domain(this, 'OpenSearchDomain', {
            version: opensearch.EngineVersion.openSearch('2.19'),
            capacity: {
                masterNodes: 0,
                dataNodes: 1,
                dataNodeInstanceType: 't3.small.search',
            },
            ebs: {
                volumeSize: 10,
                volumeType: ec2.EbsDeviceVolumeType.GP3,
            },
            zoneAwareness: {
                enabled: false,
            },
            enforceHttps: true,
            nodeToNodeEncryption: true,
            encryptionAtRest: {
                enabled: true,
            },
            fineGrainedAccessControl: {
                masterUserName: props.openSearchUsername,
                masterUserPassword: cdk.SecretValue.unsafePlainText(props.openSearchPassword),
            },
            accessPolicies: [
                new iam.PolicyStatement({
                    actions: ['es:*'],
                    resources: ['*'],
                    effect: iam.Effect.ALLOW,
                    principals: [new iam.AnyPrincipal()],
                }),
            ],
            // 移除VPC相关配置，使用公共访问模式
            removalPolicy: cdk.RemovalPolicy.DESTROY, // 注意：生产环境不建议使用DESTROY
        });
        // 创建配置文件
        const configFilePath = path.join(__dirname, '..', 'opensearch-config.json');
        const configContent = {
            domain: domain.domainName,
            endpoint: domain.domainEndpoint,
            username: props.openSearchUsername,
            password: '******',
            version: '2.19',
            region: this.region || 'cn-northwest-1',
            accessType: 'PUBLIC', // 标记为公共访问模式
        };
        // 输出配置到文件
        fs.writeFileSync(configFilePath, JSON.stringify(configContent, null, 2));
        // 输出重要信息
        new cdk.CfnOutput(this, 'OpenSearchDomainEndpoint', {
            value: domain.domainEndpoint,
            description: 'OpenSearch domain endpoint',
        });
        new cdk.CfnOutput(this, 'OpenSearchDashboardsURL', {
            value: `https://${domain.domainEndpoint}/_dashboards/`,
            description: 'OpenSearch Dashboards URL',
        });
        new cdk.CfnOutput(this, 'OpenSearchUsername', {
            value: props.openSearchUsername,
            description: 'OpenSearch master username',
        });
        new cdk.CfnOutput(this, 'ConfigFilePath', {
            value: configFilePath,
            description: 'Path to the OpenSearch configuration file',
        });
    }
}
exports.AosPublicSetupStack = AosPublicSetupStack;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiYW9zLXB1YmxpYy1zZXR1cC1zdGFjay5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbImFvcy1wdWJsaWMtc2V0dXAtc3RhY2sudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7O0FBQUEsbUNBQW1DO0FBRW5DLGdFQUFnRTtBQUNoRSwyQ0FBMkM7QUFDM0MsMkNBQTJDO0FBQzNDLHlCQUF5QjtBQUN6Qiw2QkFBNkI7QUFPN0IsTUFBYSxtQkFBb0IsU0FBUSxHQUFHLENBQUMsS0FBSztJQUNoRCxZQUFZLEtBQWdCLEVBQUUsRUFBVSxFQUFFLEtBQStCO1FBQ3ZFLEtBQUssQ0FBQyxLQUFLLEVBQUUsRUFBRSxFQUFFLEtBQUssQ0FBQyxDQUFDO1FBRXhCLG1DQUFtQztRQUNuQyxNQUFNLE1BQU0sR0FBRyxJQUFJLFVBQVUsQ0FBQyxNQUFNLENBQUMsSUFBSSxFQUFFLGtCQUFrQixFQUFFO1lBQzdELE9BQU8sRUFBRSxVQUFVLENBQUMsYUFBYSxDQUFDLFVBQVUsQ0FBQyxNQUFNLENBQUM7WUFDcEQsUUFBUSxFQUFFO2dCQUNSLFdBQVcsRUFBRSxDQUFDO2dCQUNkLFNBQVMsRUFBRSxDQUFDO2dCQUNaLG9CQUFvQixFQUFFLGlCQUFpQjthQUN4QztZQUNELEdBQUcsRUFBRTtnQkFDSCxVQUFVLEVBQUUsRUFBRTtnQkFDZCxVQUFVLEVBQUUsR0FBRyxDQUFDLG1CQUFtQixDQUFDLEdBQUc7YUFDeEM7WUFDRCxhQUFhLEVBQUU7Z0JBQ2IsT0FBTyxFQUFFLEtBQUs7YUFDZjtZQUNELFlBQVksRUFBRSxJQUFJO1lBQ2xCLG9CQUFvQixFQUFFLElBQUk7WUFDMUIsZ0JBQWdCLEVBQUU7Z0JBQ2hCLE9BQU8sRUFBRSxJQUFJO2FBQ2Q7WUFDRCx3QkFBd0IsRUFBRTtnQkFDeEIsY0FBYyxFQUFFLEtBQUssQ0FBQyxrQkFBa0I7Z0JBQ3hDLGtCQUFrQixFQUFFLEdBQUcsQ0FBQyxXQUFXLENBQUMsZUFBZSxDQUFDLEtBQUssQ0FBQyxrQkFBa0IsQ0FBQzthQUM5RTtZQUNELGNBQWMsRUFBRTtnQkFDZCxJQUFJLEdBQUcsQ0FBQyxlQUFlLENBQUM7b0JBQ3RCLE9BQU8sRUFBRSxDQUFDLE1BQU0sQ0FBQztvQkFDakIsU0FBUyxFQUFFLENBQUMsR0FBRyxDQUFDO29CQUNoQixNQUFNLEVBQUUsR0FBRyxDQUFDLE1BQU0sQ0FBQyxLQUFLO29CQUN4QixVQUFVLEVBQUUsQ0FBQyxJQUFJLEdBQUcsQ0FBQyxZQUFZLEVBQUUsQ0FBQztpQkFDckMsQ0FBQzthQUNIO1lBQ0QscUJBQXFCO1lBQ3JCLGFBQWEsRUFBRSxHQUFHLENBQUMsYUFBYSxDQUFDLE9BQU8sRUFBRSxzQkFBc0I7U0FDakUsQ0FBQyxDQUFDO1FBRUgsU0FBUztRQUNULE1BQU0sY0FBYyxHQUFHLElBQUksQ0FBQyxJQUFJLENBQUMsU0FBUyxFQUFFLElBQUksRUFBRSx3QkFBd0IsQ0FBQyxDQUFDO1FBQzVFLE1BQU0sYUFBYSxHQUFHO1lBQ3BCLE1BQU0sRUFBRSxNQUFNLENBQUMsVUFBVTtZQUN6QixRQUFRLEVBQUUsTUFBTSxDQUFDLGNBQWM7WUFDL0IsUUFBUSxFQUFFLEtBQUssQ0FBQyxrQkFBa0I7WUFDbEMsUUFBUSxFQUFFLFFBQVE7WUFDbEIsT0FBTyxFQUFFLE1BQU07WUFDZixNQUFNLEVBQUUsSUFBSSxDQUFDLE1BQU0sSUFBSSxnQkFBZ0I7WUFDdkMsVUFBVSxFQUFFLFFBQVEsRUFBRSxZQUFZO1NBQ25DLENBQUM7UUFFRixVQUFVO1FBQ1YsRUFBRSxDQUFDLGFBQWEsQ0FBQyxjQUFjLEVBQUUsSUFBSSxDQUFDLFNBQVMsQ0FBQyxhQUFhLEVBQUUsSUFBSSxFQUFFLENBQUMsQ0FBQyxDQUFDLENBQUM7UUFFekUsU0FBUztRQUNULElBQUksR0FBRyxDQUFDLFNBQVMsQ0FBQyxJQUFJLEVBQUUsMEJBQTBCLEVBQUU7WUFDbEQsS0FBSyxFQUFFLE1BQU0sQ0FBQyxjQUFjO1lBQzVCLFdBQVcsRUFBRSw0QkFBNEI7U0FDMUMsQ0FBQyxDQUFDO1FBRUgsSUFBSSxHQUFHLENBQUMsU0FBUyxDQUFDLElBQUksRUFBRSx5QkFBeUIsRUFBRTtZQUNqRCxLQUFLLEVBQUUsV0FBVyxNQUFNLENBQUMsY0FBYyxlQUFlO1lBQ3RELFdBQVcsRUFBRSwyQkFBMkI7U0FDekMsQ0FBQyxDQUFDO1FBRUgsSUFBSSxHQUFHLENBQUMsU0FBUyxDQUFDLElBQUksRUFBRSxvQkFBb0IsRUFBRTtZQUM1QyxLQUFLLEVBQUUsS0FBSyxDQUFDLGtCQUFrQjtZQUMvQixXQUFXLEVBQUUsNEJBQTRCO1NBQzFDLENBQUMsQ0FBQztRQUVILElBQUksR0FBRyxDQUFDLFNBQVMsQ0FBQyxJQUFJLEVBQUUsZ0JBQWdCLEVBQUU7WUFDeEMsS0FBSyxFQUFFLGNBQWM7WUFDckIsV0FBVyxFQUFFLDJDQUEyQztTQUN6RCxDQUFDLENBQUM7SUFDTCxDQUFDO0NBQ0Y7QUE1RUQsa0RBNEVDIiwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICogYXMgY2RrIGZyb20gJ2F3cy1jZGstbGliJztcbmltcG9ydCB7IENvbnN0cnVjdCB9IGZyb20gJ2NvbnN0cnVjdHMnO1xuaW1wb3J0ICogYXMgb3BlbnNlYXJjaCBmcm9tICdhd3MtY2RrLWxpYi9hd3Mtb3BlbnNlYXJjaHNlcnZpY2UnO1xuaW1wb3J0ICogYXMgZWMyIGZyb20gJ2F3cy1jZGstbGliL2F3cy1lYzInO1xuaW1wb3J0ICogYXMgaWFtIGZyb20gJ2F3cy1jZGstbGliL2F3cy1pYW0nO1xuaW1wb3J0ICogYXMgZnMgZnJvbSAnZnMnO1xuaW1wb3J0ICogYXMgcGF0aCBmcm9tICdwYXRoJztcblxuZXhwb3J0IGludGVyZmFjZSBBb3NQdWJsaWNTZXR1cFN0YWNrUHJvcHMgZXh0ZW5kcyBjZGsuU3RhY2tQcm9wcyB7XG4gIG9wZW5TZWFyY2hVc2VybmFtZTogc3RyaW5nO1xuICBvcGVuU2VhcmNoUGFzc3dvcmQ6IHN0cmluZztcbn1cblxuZXhwb3J0IGNsYXNzIEFvc1B1YmxpY1NldHVwU3RhY2sgZXh0ZW5kcyBjZGsuU3RhY2sge1xuICBjb25zdHJ1Y3RvcihzY29wZTogQ29uc3RydWN0LCBpZDogc3RyaW5nLCBwcm9wczogQW9zUHVibGljU2V0dXBTdGFja1Byb3BzKSB7XG4gICAgc3VwZXIoc2NvcGUsIGlkLCBwcm9wcyk7XG5cbiAgICAvLyDliJvlu7pPcGVuU2VhcmNo5Z+fIC0g5L2/55So5YWs5YWx6K6/6Zeu5qih5byP77yI5LiN5ZyoVlBD5YaF77yJXG4gICAgY29uc3QgZG9tYWluID0gbmV3IG9wZW5zZWFyY2guRG9tYWluKHRoaXMsICdPcGVuU2VhcmNoRG9tYWluJywge1xuICAgICAgdmVyc2lvbjogb3BlbnNlYXJjaC5FbmdpbmVWZXJzaW9uLm9wZW5TZWFyY2goJzIuMTknKSxcbiAgICAgIGNhcGFjaXR5OiB7XG4gICAgICAgIG1hc3Rlck5vZGVzOiAwLFxuICAgICAgICBkYXRhTm9kZXM6IDEsXG4gICAgICAgIGRhdGFOb2RlSW5zdGFuY2VUeXBlOiAndDMuc21hbGwuc2VhcmNoJyxcbiAgICAgIH0sXG4gICAgICBlYnM6IHtcbiAgICAgICAgdm9sdW1lU2l6ZTogMTAsXG4gICAgICAgIHZvbHVtZVR5cGU6IGVjMi5FYnNEZXZpY2VWb2x1bWVUeXBlLkdQMyxcbiAgICAgIH0sXG4gICAgICB6b25lQXdhcmVuZXNzOiB7XG4gICAgICAgIGVuYWJsZWQ6IGZhbHNlLFxuICAgICAgfSxcbiAgICAgIGVuZm9yY2VIdHRwczogdHJ1ZSxcbiAgICAgIG5vZGVUb05vZGVFbmNyeXB0aW9uOiB0cnVlLFxuICAgICAgZW5jcnlwdGlvbkF0UmVzdDoge1xuICAgICAgICBlbmFibGVkOiB0cnVlLFxuICAgICAgfSxcbiAgICAgIGZpbmVHcmFpbmVkQWNjZXNzQ29udHJvbDoge1xuICAgICAgICBtYXN0ZXJVc2VyTmFtZTogcHJvcHMub3BlblNlYXJjaFVzZXJuYW1lLFxuICAgICAgICBtYXN0ZXJVc2VyUGFzc3dvcmQ6IGNkay5TZWNyZXRWYWx1ZS51bnNhZmVQbGFpblRleHQocHJvcHMub3BlblNlYXJjaFBhc3N3b3JkKSxcbiAgICAgIH0sXG4gICAgICBhY2Nlc3NQb2xpY2llczogW1xuICAgICAgICBuZXcgaWFtLlBvbGljeVN0YXRlbWVudCh7XG4gICAgICAgICAgYWN0aW9uczogWydlczoqJ10sXG4gICAgICAgICAgcmVzb3VyY2VzOiBbJyonXSxcbiAgICAgICAgICBlZmZlY3Q6IGlhbS5FZmZlY3QuQUxMT1csXG4gICAgICAgICAgcHJpbmNpcGFsczogW25ldyBpYW0uQW55UHJpbmNpcGFsKCldLFxuICAgICAgICB9KSxcbiAgICAgIF0sXG4gICAgICAvLyDnp7vpmaRWUEPnm7jlhbPphY3nva7vvIzkvb/nlKjlhazlhbHorr/pl67mqKHlvI9cbiAgICAgIHJlbW92YWxQb2xpY3k6IGNkay5SZW1vdmFsUG9saWN5LkRFU1RST1ksIC8vIOazqOaEj++8mueUn+S6p+eOr+Wig+S4jeW7uuiuruS9v+eUqERFU1RST1lcbiAgICB9KTtcblxuICAgIC8vIOWIm+W7uumFjee9ruaWh+S7tlxuICAgIGNvbnN0IGNvbmZpZ0ZpbGVQYXRoID0gcGF0aC5qb2luKF9fZGlybmFtZSwgJy4uJywgJ29wZW5zZWFyY2gtY29uZmlnLmpzb24nKTtcbiAgICBjb25zdCBjb25maWdDb250ZW50ID0ge1xuICAgICAgZG9tYWluOiBkb21haW4uZG9tYWluTmFtZSxcbiAgICAgIGVuZHBvaW50OiBkb21haW4uZG9tYWluRW5kcG9pbnQsXG4gICAgICB1c2VybmFtZTogcHJvcHMub3BlblNlYXJjaFVzZXJuYW1lLFxuICAgICAgcGFzc3dvcmQ6ICcqKioqKionLCAvLyDkuI3lrZjlgqjlrp7pmYXlr4bnoIFcbiAgICAgIHZlcnNpb246ICcyLjE5JyxcbiAgICAgIHJlZ2lvbjogdGhpcy5yZWdpb24gfHwgJ2NuLW5vcnRod2VzdC0xJyxcbiAgICAgIGFjY2Vzc1R5cGU6ICdQVUJMSUMnLCAvLyDmoIforrDkuLrlhazlhbHorr/pl67mqKHlvI9cbiAgICB9O1xuXG4gICAgLy8g6L6T5Ye66YWN572u5Yiw5paH5Lu2XG4gICAgZnMud3JpdGVGaWxlU3luYyhjb25maWdGaWxlUGF0aCwgSlNPTi5zdHJpbmdpZnkoY29uZmlnQ29udGVudCwgbnVsbCwgMikpO1xuXG4gICAgLy8g6L6T5Ye66YeN6KaB5L+h5oGvXG4gICAgbmV3IGNkay5DZm5PdXRwdXQodGhpcywgJ09wZW5TZWFyY2hEb21haW5FbmRwb2ludCcsIHtcbiAgICAgIHZhbHVlOiBkb21haW4uZG9tYWluRW5kcG9pbnQsXG4gICAgICBkZXNjcmlwdGlvbjogJ09wZW5TZWFyY2ggZG9tYWluIGVuZHBvaW50JyxcbiAgICB9KTtcblxuICAgIG5ldyBjZGsuQ2ZuT3V0cHV0KHRoaXMsICdPcGVuU2VhcmNoRGFzaGJvYXJkc1VSTCcsIHtcbiAgICAgIHZhbHVlOiBgaHR0cHM6Ly8ke2RvbWFpbi5kb21haW5FbmRwb2ludH0vX2Rhc2hib2FyZHMvYCxcbiAgICAgIGRlc2NyaXB0aW9uOiAnT3BlblNlYXJjaCBEYXNoYm9hcmRzIFVSTCcsXG4gICAgfSk7XG5cbiAgICBuZXcgY2RrLkNmbk91dHB1dCh0aGlzLCAnT3BlblNlYXJjaFVzZXJuYW1lJywge1xuICAgICAgdmFsdWU6IHByb3BzLm9wZW5TZWFyY2hVc2VybmFtZSxcbiAgICAgIGRlc2NyaXB0aW9uOiAnT3BlblNlYXJjaCBtYXN0ZXIgdXNlcm5hbWUnLFxuICAgIH0pO1xuXG4gICAgbmV3IGNkay5DZm5PdXRwdXQodGhpcywgJ0NvbmZpZ0ZpbGVQYXRoJywge1xuICAgICAgdmFsdWU6IGNvbmZpZ0ZpbGVQYXRoLFxuICAgICAgZGVzY3JpcHRpb246ICdQYXRoIHRvIHRoZSBPcGVuU2VhcmNoIGNvbmZpZ3VyYXRpb24gZmlsZScsXG4gICAgfSk7XG4gIH1cbn1cbiJdfQ==