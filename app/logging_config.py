import logging


def configure_logging(level: int | str = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)



