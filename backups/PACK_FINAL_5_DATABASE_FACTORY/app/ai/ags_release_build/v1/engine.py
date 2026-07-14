class AGSReleaseBuild:
    def release(self,data):
        return {
            "engine":"AGS_RELEASE_BUILD_V1",
            "status":"released",
            "version":"1.0",
            "system":data
        }
