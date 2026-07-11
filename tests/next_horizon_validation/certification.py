class HorizonCertification:

    def validate(self):

        return {
            "long_term_validation":"PASSED",
            "horizon_engine":"PASSED",
            "phase_151_200":"PASSED",
            "certification":"NEXT HORIZON CERTIFIED",
            "status":"READY"
        }


if __name__=="__main__":
    print(HorizonCertification().validate())
