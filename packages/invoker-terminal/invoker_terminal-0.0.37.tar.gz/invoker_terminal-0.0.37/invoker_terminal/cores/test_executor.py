import uuid
import os
from pathlib import Path
import json
import io
import zipfile
import docker
import shutil


class TestExecutor:
    def __init__(self, input) -> None:
        self.input = input
    
    def run(self):
        id = uuid.uuid4()
        config = TestExecutor.config
        args = TestExecutor.args        
        host_url = os.path.join(config["system"]["tmp_folder"], str(id))
        Path(host_url).mkdir(parents=True, exist_ok=True)
        fmtinput = json.dumps(self.input)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(
            zip_buffer, "a", zipfile.ZIP_DEFLATED, False
        ) as zip_file:
            for file_name, data in [
                ("input/desc.json", io.BytesIO(fmtinput.encode("utf-8"))),
            ]:
                zip_file.writestr(file_name, data.getvalue())

        with open("{}/input.zip".format(host_url), "wb") as f:
            f.write(zip_buffer.getvalue())

        client = docker.DockerClient(base_url=config["system"]["docker_url"])
        volumes = [host_url]
        volume_bindings = {
            "{}".format(host_url): {
                "bind": "/invoker",
                "mode": "rw",
            },
        }
        device_requests = []
        gpu_enabled = config["system"].get("gpu_enabled", False)
        if gpu_enabled != "False" and gpu_enabled != False:
            device_requests = [docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])]
        
        host_config = client.api.create_host_config(
            binds=volume_bindings,
            device_requests=device_requests)
        try:
            f = json.load(open("./build.json"))
        except:
            print("build the project first!!!")
            os._exit(-1)
        container = client.api.create_container(
            f["id"], volumes=volumes, host_config=host_config
        )
        print("Running Imgage({}) on Container ({})".format(f["id"][0:12],container.get("Id")[0:6]))
        client.api.start(container=container.get("Id"))
        client.api.wait(container)
        logs = client.api.logs(container=container.get("Id"))
        print("Container ({}) Logs".format(container.get("Id")))
        print("------------------")
        print(logs.decode("utf-8"))
        print("------------------")
        outputfile = "{}/output.zip".format(host_url)
        output = {}
        # opening the zip file in READ mode
        with zipfile.ZipFile(outputfile, 'r') as zip:
            # printing all the contents of the zip file
            zip.printdir()
            for file in zip.filelist:
                if file.filename.startswith("output/"):
                    ff = file.filename.split("output/")
                    output[ff[1]] = zip.read(file.filename)
        try:
            client.api.remove_container(container, True, False, True)
            shutil.rmtree(host_url)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
        
        return output