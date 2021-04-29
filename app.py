from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask import request
from flask import url_for
from flask import session
import docker
from docker import tls
import ssl

app = Flask(__name__)
app.secret_key = '123'
bootstrap = Bootstrap(app)


@app.route('/', methods=['POST', 'GET'])
def first():
    Restart_button = request.form.get('restart')    #获取重启按钮提交的表单数据：默认为None，如果点击重启按钮，则为对应容器ID。
    if request.method == 'POST':    #判断请求路由的方法是否为POST
        server_ip = request.form.get('server')  #获取用户输入的服务器IP表单数据
        tls_config = docker.tls.TLSConfig(client_cert=('./client.crt','./client.pem'),verify='./ca.crt',ssl_version=ssl.PROTOCOL_TLSv1_2)
        try:
            client = docker.Client(base_url=f'https://{server_ip}:2376',tls=tls_config)  #连接用户指定服务器上的docker服务。
        except Exception as error1:
            return error1


        Standard_restart = None     #指定判断重启是否成功的变量
        if Restart_button:  #用户是否点击了重启按钮
            try:
                client.restart(Restart_button)  #如果点击，则执行重启指定容器
            except Exception:
                Standard_restart = False    #如果重启失败，则变量为False
            else:
                Standard_restart = True     #重启成功，则变量为True


        container_info = client.containers(all=True)   #获取全部容器的状态信息
        container_number = range(0, len(container_info))  # 从0---容器个数
        return render_template('table.html', container_info=container_info, container_number=container_number, server_ip=server_ip, Standard_restart=Standard_restart, Restart_button=Restart_button)   #返回模板，传入数据
    elif request.method == 'GET':   #如果是GET请求，则返回基础模板
        return render_template('base.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0')
