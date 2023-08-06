import pkg_resources

class VersionUtil:
    def get_version():
        return pkg_resources.get_distribution('remlalib').version