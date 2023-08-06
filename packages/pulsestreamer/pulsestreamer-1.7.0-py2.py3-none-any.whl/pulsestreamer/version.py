from pulsestreamer import __version__


def _compare_version_number(version_1, version_2=None):
        #returns True, if firmware_version_1 is equal or higher than firmware_version_2
        #if no second argument is given it compares the first argument with the next firmware version dedicated to update the current client software

        if version_2 is None:
            # next firmware version expected to update the current client software
            # next version is "<MAJOR>.<MINOR+1>.<0>..."
            current_ver = (int(n) for n in __version__.split('.'))
            next_ver = (v if i==0 else v+1 if i==1 else 0 for i,v in enumerate(current_ver))
            version_2 = '.'.join(str(v) for v in next_ver)

        # CLEANUP: Next two lines shall be moved to the point of concern.
        split_version_1 = version_1.split(' ')[0].split('.')
        split_version_2 = version_2.split(' ')[0].split('.')

        for i in range(max(len(split_version_1), len(split_version_2))):
            if i > len(split_version_1)-1:
                num1 = 0
                num2 = int(split_version_2[i])
            elif i >  len(split_version_2)-1:
                num1=int(split_version_1[i])
                num2=0
            else:
                num1=int(split_version_1[i])
                num2 = int(split_version_2[i])
            if num1 > num2:
                return 1
            elif num2 > num1:
                return -1
            else:
                continue
        return 0
