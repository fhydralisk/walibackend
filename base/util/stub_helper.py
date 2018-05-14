import re
import os


PATTERN_STUB = r'(\s*)\(\d+,[^"]*"[^"]*"[^,]*,\s*"([^"]+)"\s*\)'
PATTERN_IGNORE = r'\s*(from|import|MAX_LENGTH|CHOICE_DISPLAY|\))'


def to_stub(filename):
    p_stub = re.compile(PATTERN_STUB)
    p_ignore = re.compile(PATTERN_IGNORE)
    writelines = ["from base.util.field_choice import FieldChoice"]
    with open(filename) as f:
        lines = f.readlines()
        print("File %s opened." % filename)
        for l in lines:
            if p_ignore.match(l) is None:

                stub = p_stub.match(l)
                if stub is not None:
                    writelines.append("%s%s = None\n" % (stub.groups()[0][4:], stub.groups()[1]))
                    continue

                writelines.append(l)

        file_to_save = os.path.join(os.path.dirname(filename), os.path.basename(filename) + "i")
        with open(file_to_save, "w") as fs:
            print("File %s opened." % file_to_save)
            fs.write("".join(writelines))
