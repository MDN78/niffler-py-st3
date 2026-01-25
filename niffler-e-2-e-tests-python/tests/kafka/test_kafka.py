import json
import allure
import pytest

from http import HTTPStatus

from databases.auth_db import UserDb
from databases.userdata_db import UserdataDb
from tools.assertions.base import assert_status_code
from tools.fakers import fake
from models.user import UserName
from tools.allure.annotations import AllureEpic, AllureTags, AllureFeature, AllureStory
from tools.assertions.kafka import check_message_content, check_that_message_from_kafka_exist, \
    check_new_record_in_auth_db, check_new_record_in_user_db

pytestmark = [pytest.mark.allure_label(AllureEpic.NIFFLER, label_type="epic")]

KAFKA_TOPIC = "users"


@allure.tag(AllureTags.KAFKA)
@allure.feature(AllureFeature.KAFKA)
class TestAuthRegistrationKafka:

    @allure.story(AllureStory.KAFKA_MESSAGE)
    def test_message_should_be_produced_to_kafka_after_successful_registration(self, auth_client, kafka):
        username, password = fake.user_name(), fake.password()

        topic_partitions = kafka.subscribe_listen_new_offsets("users")
        result = auth_client.register(username, password)
        event = kafka.log_msg_and_json(topic_partitions)

        assert_status_code(result.status_code, HTTPStatus.CREATED)

        UserName.model_validate(json.loads(event.decode('utf8')))
        check_message_content(event, username)
        check_that_message_from_kafka_exist(event, '')
        check_that_message_from_kafka_exist(event, "b''")

    @allure.story(AllureStory.KAFKA_PRODUCING)
    def test_message_should_be_produced_to_userdata_after_kafka_event(self, kafka, auth_db: UserDb,
                                                                      user_db: UserdataDb):
        username = fake.user_name()

        kafka.sent_event(KAFKA_TOPIC, username)
        check_new_record_in_auth_db(auth_db, username)
        check_new_record_in_user_db(user_db, username)
