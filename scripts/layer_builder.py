import os
import shutil
import subprocess
import boto3


class LambdaLayerBuilder:
    def __init__(
        self,
        libraries: list[str],
        layer_name: str,
        python_version: str = "python3.12",
        aws_region: str = "us-east-1",
    ):
        self.libraries = libraries
        self.layer_name = layer_name
        self.python_version = python_version
        self.aws_region = aws_region
        self.layer_dir = "layer_build"
        self.python_lib_dir = os.path.join(self.layer_dir, "python")
        self.zip_name = f"{layer_name.lower()}-layer"

    def install_libraries(self):
        """Instala as bibliotecas compatíveis com AWS Lambda (ARM64)."""
        print(f"📦 Instalando {', '.join(self.libraries)} para ARM64...")
        os.makedirs(self.python_lib_dir, exist_ok=True)

        subprocess.run(
            [
                "pip",
                "install",
                "--platform",
                "manylinux2014_aarch64",
                "--only-binary=:all:",
                "--target",
                self.python_lib_dir,
                "--upgrade",
                *self.libraries,
            ],
            check=True,
        )

    def package_layer(self):
        """Compacta a layer para upload."""
        print("🗜 Compactando a Layer...")
        shutil.make_archive(self.zip_name, "zip", self.layer_dir)

    def publish_layer(self):
        """Publica a layer no AWS Lambda."""
        print("🚀 Publicando Layer na AWS...")

        lambda_client = boto3.client("lambda", region_name=self.aws_region)

        with open(f"{self.zip_name}.zip", "rb") as zip_file:
            response = lambda_client.publish_layer_version(
                LayerName=self.layer_name,
                Description=f"{', '.join(self.libraries)} para AWS Lambda ARM64",
                Content={"ZipFile": zip_file.read()},
                CompatibleRuntimes=[self.python_version],
                CompatibleArchitectures=["arm64"],
            )

        layer_arn = response["LayerVersionArn"]
        print(f"✅ Layer publicada com sucesso: {layer_arn}")
        return layer_arn

    def cleanup(self):
        """Remove arquivos temporários."""
        print("🧹 Limpando arquivos temporários...")
        shutil.rmtree(self.layer_dir, ignore_errors=True)
        os.remove(f"{self.zip_name}.zip")

    def build(self):
        """Executa todo o processo de criação e publicação da layer."""
        self.install_libraries()
        self.package_layer()
        layer_arn = self.publish_layer()
        self.cleanup()
        print("🎉 Processo concluído com sucesso!")
        return layer_arn
