class Responses(object):

    @staticmethod
    def success_response(is_success=True, message=None, data=None):
        return {
            'is_success': is_success,
            'message': message,
            'data': data
        }

    @staticmethod
    def error_response(is_success=False, message=None):
        return {
            'is_success': is_success,
            'message': message,
            'data': None
        }

    @staticmethod
    def get_response(is_success=True, message=None, data=None):
        return {
            'is_success': is_success,
            'message': message,
            'data': data
        }

    @staticmethod
    def get_client_args(active_tab=None, sub_active_tab=None, user_name=None, profile_image_path=None,
                        client_list=None, single_client_data=None):
        return {
            'user_name': user_name,
            'active_tab': active_tab,
            'sub_active_tab': sub_active_tab,
            'profile_image_path': profile_image_path,
            'client_list': client_list,
            'single_client_data': single_client_data,
        }

    @staticmethod
    def get_user_args(active_tab=None, sub_active_tab=None, user_name=None, profile_image_path=None,
                      user_list=None, single_client_data=None):
        return {
            'user_name': user_name,
            'active_tab': active_tab,
            'sub_active_tab': sub_active_tab,
            'profile_image_path': profile_image_path,
            'user_list': user_list,
            'single_client_data': single_client_data,
        }

    @staticmethod
    def get_client_role_args(active_tab=None, sub_active_tab=None, user_name=None, profile_image_path=None,
                             client_roles=None, single_client_role=None):
        return {
            'user_name': user_name,
            'active_tab': active_tab,
            'sub_active_tab': sub_active_tab,
            'profile_image_path': profile_image_path,
            'client_roles': client_roles,
            'single_client_role': single_client_role,
        }

    @staticmethod
    def get_args(active_tab=None, sub_active_tab=None, toast_type=None, toast_message='', user_name=None,
                 is_success=False, profile_image_path=None, package_types=None, privacy_types=None,
                 response_types=None, event_types=None, payment_types=None, single_package_type=None,
                 single_privacy_type=None, single_response_type=None, single_event_type=None,
                 single_payment_type=None, clients=None, service_charges=None, single_service_charge=None):
        return {
            'toast_type': toast_type,
            'toast_message': toast_message,
            'user_name': user_name,
            'active_tab': active_tab,
            'sub_active_tab': sub_active_tab,
            'is_success': is_success,
            'profile_image_path': profile_image_path,
            'package_types': package_types,
            'privacy_types': privacy_types,
            'response_types': response_types,
            'event_types': event_types,
            'payment_types': payment_types,
            'single_package_type': single_package_type,
            'single_privacy_type': single_privacy_type,
            'single_response_type': single_response_type,
            'single_event_type': single_event_type,
            'single_payment_type': single_payment_type,
            'clients': clients,
            'service_charges': service_charges,
            'single_service_charge': single_service_charge,
        }
