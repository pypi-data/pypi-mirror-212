class VersionUtil:
    def get_version():
        return open("remlalib/_version.py").readlines()[-1].split()[-1].strip("\"'")