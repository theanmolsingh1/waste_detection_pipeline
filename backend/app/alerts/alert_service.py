from app.alerts.notification import ConsoleAlert, DashboardAlert


class AlertService:
    def __init__(self, providers=None):
        self.providers = providers or [ConsoleAlert(), DashboardAlert()]

    def send_alert(self, detection: dict) -> bool:
        return all(provider.send(detection) for provider in self.providers)
