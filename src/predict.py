from src.modeling.predict import predict_default_probability
from src.logger import get_logger


logger = get_logger(__name__)


if __name__ == "__main__":

    logger.info("Starting batch prediction inference")

    try:

        results = predict_default_probability()

        logger.info(
            f"Batch prediction completed successfully | "
            f"records={len(results)}"
        )

        print("=" * 60)
        print("BATCH PREDICTION INFERENCE")
        print("=" * 60)

        print(
            f"Evaluated {len(results):,} sample applications."
        )

        print("Sample Prediction Output:")

        print(
            results[
                [
                    "Predicted_Default_Prob",
                    "Predicted_Status",
                ]
            ].head(10)
        )

        print("=" * 60)

        logger.info("Batch prediction output displayed successfully")

    except Exception as exc:

        logger.exception(
            f"Batch prediction failed | error={exc}"
        )

        raise