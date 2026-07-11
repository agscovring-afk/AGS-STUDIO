class EvolutionPhaseManager:

    def status(self):
        phases = {}

        for phase in range(61,76):
            phases[f"PHASE_{phase}"] = "READY"

        return {
            "platform":"AGS-STUDIO NEXT EVOLUTION ERA",
            "phases":"61-75",
            "status":"ACTIVE",
            "details":phases
        }


if __name__=="__main__":
    print(EvolutionPhaseManager().status())
