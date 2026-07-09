import sys
import pprint

from app.ai.self_developer.pipeline import DevelopmentPipeline


def main():

    if len(sys.argv) < 3:

        print(
            "Usage: python dev.py create <module description>"
        )

        return


    command = sys.argv[1]

    requirement = " ".join(
        sys.argv[2:]
    )


    if command == "create":

        pipeline = DevelopmentPipeline()

        result = pipeline.create(
            requirement
        )

        pprint.pp(
            result
        )

    else:

        print(
            "Unknown command"
        )


if __name__ == "__main__":

    main()
