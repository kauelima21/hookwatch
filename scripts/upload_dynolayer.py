from scripts.layer_builder import LambdaLayerBuilder

if __name__ == "__main__":
    builder = LambdaLayerBuilder(
        libraries=["dynolayer"],
        layer_name="DynoLayer",
    )
    builder.build()
