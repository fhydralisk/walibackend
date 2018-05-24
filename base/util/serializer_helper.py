"""
Helper for serializers

"""


def errors_summery(serializer):
    def iterate_err(errors, parent_field, s_field_errors):
        for field, errs in errors.items():
            if isinstance(errs, dict):
                iterate_err(errs, field + ".", s_field_errors)
            else:
                for err in errs:
                    s_field_errors.append("%s%s: %s" % (parent_field, field, err))

    field_errors = []
    iterate_err(serializer.errors, "", field_errors)

    return "Validation on request object failed, errors: %s" % ";".join(field_errors)
