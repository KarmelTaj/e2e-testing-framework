import inspect

class Assert:
    
    @staticmethod
    def _format_message(msg, standard_msg):
        """
        Formats the message to include additional context if provided.
        """
        return msg if msg else standard_msg

    @staticmethod
    def _get_call_context():
        """
        Retrieves the calling context, including the class name, method name, file name, and line number.
        """
        stack = inspect.stack()
        # Get the previous frame (caller of the assert method)
        caller_frame = stack[2]
        caller_class = caller_frame.frame.f_locals.get('self', None)
        class_name = caller_class.__class__.__name__ if caller_class else None
        method_name = caller_frame.function
        file_name = caller_frame.filename
        line_number = caller_frame.lineno

        context = f"{file_name}:{line_number} - "
        context += f"{class_name}.{method_name}" if class_name else method_name
        return context

    @staticmethod
    def assertEqual(first, second, msg=None):
        """
        Checks if the first arg matches the second arg.
        Raises an AssertionError if the check fails, including the file and line number.
        """
        if first != second:
            context = Assert._get_call_context()
            standard_msg = f"{context} - Expected {second}, but got {first}."
            raise AssertionError(Assert._format_message(msg, standard_msg))

    @staticmethod
    def assertNotEqual(first, second, msg=None):
        """
        Checks if the first arg does not match the second arg.
        """
        if first == second:
            context = Assert._get_call_context()
            standard_msg = f"{context} - Did not expect {second}, but got it."
            raise AssertionError(Assert._format_message(msg, standard_msg))

    @staticmethod
    def assertIn(item, collection, msg=None):
        """
        Checks if an item is in a collection.
        """
        if item not in collection:
            context = Assert._get_call_context()
            standard_msg = f"{context} - Expected {item} to be in {collection}."
            raise AssertionError(Assert._format_message(msg, standard_msg))

    @staticmethod
    def assertNotIn(item, collection, msg=None):
        """
        Checks if an item is not in a collection.
        """
        if item in collection:
            context = Assert._get_call_context()
            standard_msg = f"{context} - Did not expect {item} to be in {collection}."
            raise AssertionError(Assert._format_message(msg, standard_msg))

    @staticmethod
    def assertGreaterThan(value, greater_value, msg=None):
        """
        Checks if a value is greater than a greater_value.
        """
        if value <= greater_value:
            context = Assert._get_call_context()
            standard_msg = f"{context} - Expected {value} to be greater than {greater_value}."
            raise AssertionError(Assert._format_message(msg, standard_msg))

    @staticmethod
    def assertLessThan(value, lesser_value, msg=None):
        """
        Checks if a value is less than a lesser_value.
        """
        if value >= lesser_value:
            context = Assert._get_call_context()
            standard_msg = f"{context} - Expected {value} to be less than {lesser_value}."
            raise AssertionError(Assert._format_message(msg, standard_msg))

    @staticmethod
    def assertNotNull(value, msg=None):
        """
        Checks if a value is not null (None).
        """
        if value is None:
            context = Assert._get_call_context()
            standard_msg = f"{context} - Expected value to not be null, but got None."
            raise AssertionError(Assert._format_message(msg, standard_msg))
