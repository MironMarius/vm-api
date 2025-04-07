class ResponseBuilder:
    OK_STATUS = 'ok'
    ERROR_STATUS = 'error'
    NOT_FOUND_STATUS = 'not_found'

    @classmethod
    def machine_not_found(cls, machine_id):
        return cls.build(
            cls.NOT_FOUND_STATUS,
            f"Machine with id: {machine_id} not found"
        )

    @classmethod
    def machine_created_successfully(cls, machine_id):
        return cls.build(
            cls.OK_STATUS,
            'Machine created successfully',
            machine_id=machine_id
        )

    @classmethod
    def ok(cls, msg):
        return cls.build(
            cls.OK_STATUS,
            msg
        )

    @classmethod
    def error(cls, msg, **kwargs):
        return cls.build(
            cls.ERROR_STATUS,
            msg,
            **kwargs
        )

    @staticmethod
    def build(status, msg, **kwargs):
        return {
            'status': status,
            'msg': msg.strip(),
             **kwargs
        }
