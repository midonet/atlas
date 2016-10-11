
from fabric.api import run

class ServiceControl(object):
    def __init__(self):
        return

    @classmethod
    def launch(cls, service_name, process_name=None):
        if process_name == None:
            process_name = service_name

        run("""
SERVICE_NAME="%s"
PROCESS_NAME="%s"

# update-rc.d "${SERVICE_NAME}" defaults
# /etc/init.d/"${SERVICE_NAME}" restart
# service "${SERVICE_NAME}" restart

systemctl restart "${SERVICE_NAME}"

for i in $(seq 1 120); do
    ps axufwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww | grep -v grep | grep "${PROCESS_NAME}" && break
    sleep 1
done

ps axufwwwwwwwww | grep -v grep | grep "${PROCESS_NAME}"

""" % (service_name, process_name))

