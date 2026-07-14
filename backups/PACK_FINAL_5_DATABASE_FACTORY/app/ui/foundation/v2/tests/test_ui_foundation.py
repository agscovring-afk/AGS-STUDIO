def run_ui_foundation_test():

    from app.ui.foundation.v2.responsive.responsive_engine import ResponsiveLayoutEngine
    from app.ui.foundation.v2.events.event_bus import EventBus
    from app.ui.foundation.v2.state.ui_state_manager import UIStateManager

    ResponsiveLayoutEngine()
    EventBus()
    UIStateManager()

    return "UI FOUNDATION V2 OK"


if __name__ == "__main__":

    print(run_ui_foundation_test())
