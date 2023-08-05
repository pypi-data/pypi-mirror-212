from app.config import Configurator, ConverterOptions


def make_fake_configurator(converter: str, converter_options: ConverterOptions):
    class FakeConfigurator(Configurator):
        logging_level: str = "INFO"
        source_path: str = ""
        output_path: str = ""
        converter: str = ""
        converter_options = ConverterOptions(
            author_rewrite="",
            links_rewrite=[],
            header_fields_drop=[],
        )

        class Config:
            env_file_encoding = "utf-8"

            @classmethod
            def customise_sources(
                cls,
                init_settings,
                env_settings,
                file_secret_settings,
            ):
                return (init_settings,)

    configurator = FakeConfigurator()
    configurator.converter_options = converter_options
    return configurator
