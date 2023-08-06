import logging
import sys
import email_cleaning_service.data_model.data as data
import email_cleaning_service.data_model.pipelining as pipe
import email_cleaning_service.utils.request_classes as rq
from typing import List
import email_cleaning_service.services.segmenting_service as seg
import email_cleaning_service.services.training_service as train
import mlflow


class EmailCleaner:
    """Controller class for the API. Used to control the pipeline and dataset objects."""

    def __init__(self, tracking_uri: str = "https://mentis.io/mlflow/"):
        mlflow.set_tracking_uri(tracking_uri)
        logging.info("Controller initialized")

    def segment(
        self, thread_list: List[str], pipeline_specs: rq.PipelineSpecs
    ) -> data.EmailDataset:
        """Used to segment all EmailThread objects in the dataset
        pipeline must be a valid PipelineModel object
        """
        dataset = data.EmailDataset(thread_list)
        if pipeline_specs.origin == "hugg":
            pipeline = pipe.PipelineModel.from_hugg(pipeline_specs)
        elif pipeline_specs.origin == "mlflow":
            pipeline = pipe.PipelineModel.from_mlflow(pipeline_specs)
        else:
            raise ValueError("Invalid pipeline origin")
        seg.segment(dataset, pipeline)
        return dataset

    def train_classifier(
        self, run_specs: rq.RunSpecs, pipeline_specs: rq.PipelineSpecs
    ):
        """Used to train the classifier on the dataset
        pipeline must be a valid PipelineModel object
        """
        dataset = data.EmailDataset.from_csv(run_specs.csv_path)
        if pipeline_specs.origin == "hugg":
            pipeline = pipe.PipelineModel.from_hugg(pipeline_specs)
        elif pipeline_specs.origin == "mlflow":
            pipeline = pipe.PipelineModel.from_mlflow(pipeline_specs)
        else:
            raise ValueError("Invalid pipeline origin")
        train.train_classifier(run_specs, dataset, pipeline)

    def train_encoder(self, run_specs: rq.RunSpecs, encoder_specs: rq.EncoderSpecs):
        """Used to train the encoder on the dataset
        pipeline must be a valid PipelineModel object
        """
        dataset = data.EmailLineDataset.from_csv(run_specs.csv_path)
        if encoder_specs.origin == "hugg":
            encoder = pipe.EncoderModel.from_hugg(encoder_specs.encoder)
        elif encoder_specs.origin == "mlflow":
            encoder = pipe.EncoderModel.from_mlflow(encoder_specs.encoder)
        else:
            raise ValueError("Invalid encoder origin")
        train.train_encoder(run_specs, dataset, encoder)  # type: ignore


if __name__ == "__main__":

    tracking_uri = "https://mentis.io/mlflow/" if len(sys.argv) < 2 else sys.argv[1]

    emailCleaner = EmailCleaner()

    # Example of how to segment a dataset

    thread_list = [
        "This is a test email. I am testing the email cleaner.",
        "This is another test email with two lines.\n I am testing the email cleaner.",
    ]

    pipeline_specs = rq.PipelineSpecs(
        origin="hugg",
        classifier_id="a1f66311816e417cb94db7c2457b25d1"
    )

    dataset = emailCleaner.segment(thread_list, pipeline_specs)
    print(dataset.to_dict())

    # TODO: add testing for training


