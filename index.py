import json
import app  # 导入你的 Flask 应用

def handler(event, context):
    # 从事件中提取 HTTP 请求信息
    path = event.get('path', '')
    http_method = event.get('httpMethod', 'GET')
    query_parameters = event.get('queryParameters', {})
    body = event.get('body', '{}')
    headers = event.get('headers', {})
    
    # 创建 Flask 测试客户端来模拟请求
    with app.app.test_client() as client:
        # 根据 HTTP 方法调用相应的 Flask 路由
        if http_method == 'GET':
            response = client.get(path, query_string=query_parameters)
        elif http_method == 'POST':
            response = client.post(
                path, 
                data=body,
                content_type='application/json',
                query_string=query_parameters
            )
        elif http_method == 'PUT':
            response = client.put(
                path,
                data=body,
                content_type='application/json',
                query_string=query_parameters
            )
        elif http_method == 'DELETE':
            response = client.delete(path, query_string=query_parameters)
        else:
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        # 返回函数计算格式的响应
        return {
            'statusCode': response.status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': response.get_data(as_text=True)
        }