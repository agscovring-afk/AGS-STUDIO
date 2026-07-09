import sys

from app.ai.self_developer.pipeline import DevelopmentPipeline


def main():

    if len(sys.argv) < 3:

        print("Usage: python dev.py create <module>")

        return


    command = sys.argv[1]


    if command != "create":

        print("Unknown command")

        return


    requirement = " ".join(sys.argv[2:])


    pipeline = DevelopmentPipeline()

    result = pipeline.create(requirement)

    print(result)


if __name__ == "__main__":

    main()
