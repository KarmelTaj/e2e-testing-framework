from scenario_tester.scenarios import BaseScenario
from .endpoints import MessagingEndpoints
from scenario_tester.assertions import Assert
from scenario_tester.services import time
import os
from django.apps import apps

class MessagingTestScenario(BaseScenario):
    """
    Create and test Messaging module
    """
    def run(self):
        # Log in as partner 1
        self.set_step("Login")
        _, status_code = self.login("partner1", MessagingEndpoints.LOGIN)
        Assert.assertEqual(status_code, 200)
        
        self.set_step("Get partnet 1 profile")
        profile_res, status_code = self.call(MessagingEndpoints.GET_PROFILE)
        Assert.assertEqual(status_code, 200)
        Assert.assertIn("id", profile_res)
        partner1_id = profile_res["id"]
        
        # Log in as partner 2
        self.set_step("Login")
        self.logout()
        _, status_code = self.login("partner2", MessagingEndpoints.LOGIN)
        Assert.assertEqual(status_code, 200)
        
        self.set_step("Step 4: Get partner 2 profile")
        profile_res, status_code = self.call(MessagingEndpoints.GET_PROFILE)
        Assert.assertEqual(status_code, 200)
        Assert.assertIn("id", profile_res)
        partner2_id = profile_res["id"]
             
        # Send message from partner 2 to partner 1
        self.set_step("Send message as partnet 2")
        message_data = {
            "receiver": partner1_id,    
            "text": f"[message] {time.current_time()}",
        }
        files = {"image": None} # Because the content type is multipart/form-data we need to pass a file
        message_res, status_code = self.call(MessagingEndpoints.SEND_PRIVATE_MESSAGE, message_data, files=files)
        Assert.assertEqual(status_code, 200, message_res)
        
        # Second message
        message_data["text"] = f"[message] {time.current_time()}"
        message_res, status_code = self.call(MessagingEndpoints.SEND_PRIVATE_MESSAGE, message_data, files=files)
        Assert.assertEqual(status_code, 200, message_res)
        
        # Send message with image
        self.set_step("Step 6: Send message with image")
        image_name = "coffee-time.jpg"
        current_time = time.current_time() # So we can use it in Asserts
        message_data["text"] = f"[message with image] {current_time}"
        message_res = self.send_message_with_image(image_name, message_data)
        
        # login as partner 1 and send message to partner 2
        self.set_step("Send message as partner 1")
        self.logout()
        _, status_code = self.login("partner1", MessagingEndpoints.LOGIN)
        Assert.assertEqual(status_code, 200)
        
        message_data = {
            "receiver": partner2_id,
            "text": f"[message] {time.current_time()}"
        }
        message_res, status_code = self.call(MessagingEndpoints.SEND_PRIVATE_MESSAGE, message_data, files=files)
        Assert.assertEqual(status_code, 200)
        
        # Second message
        message_data["text"] = f"[message] {time.current_time()}"
        message_res, status_code = self.call(MessagingEndpoints.SEND_PRIVATE_MESSAGE, message_data, files=files)
        Assert.assertEqual(status_code, 200)
        
        # Send message with image
        self.set_step("Send message with image")
        image_name = "brainstorm.jpg"
        message_data["text"] = f"[message with image] {time.current_time()}"
        message_res = self.send_message_with_image(image_name, message_data)
        
        # Delete a message
        message_id = message_res["id"]
        self.set_step("Delete message")
        delete_message_endpoint = self.format_endpoint(MessagingEndpoints.DELETE_PRIVATE_MESSAGE, id=message_id)
        _, status_code = self.call(delete_message_endpoint)
        Assert.assertEqual(status_code, 204)
        
        # Send message from partner 1 to partner 1
        self.set_step("Send message as partnet 1 to partner 1")
        message_data = {
            "receiver": partner1_id,
            "text": f"[message] {time.current_time()}",
        }
        files = {"image": None}
        message_res, status_code = self.call(MessagingEndpoints.SEND_PRIVATE_MESSAGE, message_data, files=files)
        Assert.assertEqual(status_code, 200, message_res)
        
    def send_message_with_image(self, image_name: str, message_data) -> str:
        """
        Uploads a single image from the ./photos folder
        """
        photos_dir = os.path.join(apps.get_app_config("messaging").path, "photos")
        image_path = os.path.join(photos_dir, image_name)
        
        try:
            with open(image_path, "rb") as file:
                files = {"image": file}
                message_res, status_code = self.call(MessagingEndpoints.SEND_PRIVATE_MESSAGE, message_data, files=files)
                Assert.assertEqual(status_code, 200, message_res)
                return message_res
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {image_path}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading the image: {e}")
