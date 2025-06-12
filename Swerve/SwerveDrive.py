from SwerveModule import SwerveModule

class SwerveDrive:
    def __init__(self):
        self.modules = [
            SwerveModule(drive_id=11, steer_id=12),
            SwerveModule(drive_id=13, steer_id=14),
            SwerveModule(drive_id=15, steer_id=16),
            SwerveModule(drive_id=17, steer_id=18),
        ]

    def main():
        print("L bozo")