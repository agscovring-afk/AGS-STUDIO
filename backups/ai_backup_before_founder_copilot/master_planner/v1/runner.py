from .production_pipeline import ProductionPipeline

def run_production():

    pipeline = ProductionPipeline()

    return pipeline.run()
