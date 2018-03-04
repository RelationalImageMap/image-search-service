#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from google.cloud import pubsub

subscriber = pubsub.SubscriberClient()
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    topic='MY_TOPIC_NAME',  # Set this to something appropriate.
)
subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    sub='MY_SUBSCRIPTION_NAME',  # Set this to something appropriate.
)
subscriber.create_subscription(
    name=subscription_name, topic=topic_name)
subscription = subscriber.subscribe(subscription_name)


def callback(message):
	#def run_quickstart():
	# [START vision_quickstart]
	import io
	import os

	# Imports the Google Cloud client library
	# [START migration_import]
	from google.cloud import vision
	from google.cloud.vision import types
	# [END migration_import]

	# Instantiates a client
	# [START migration_client]
	client = vision.ImageAnnotatorClient()
	# [END migration_client]

	# The name of the image file to annotate
	#file_name = os.path.join(
	#	os.path.dirname(__file__),
	#	'resources/wakeupcat.jpg')

	# Loads the image into memory
	#with io.open(file_name, 'rb') as image_file:
	#	content = image_file.read()

	image = types.Image(content=message.data)

	# Performs label detection on the image file
	response = client.label_detection(image=image)
	labels = response.label_annotations

	print('Labels:')
	for label in labels:
		print(label.description)
	# [END vision_quickstart]
	message.ack()
subscription.open(callback)

if __name__ == '__main__':
    callback()
