import logging
import lib.config.placeholder as appConfig
from lib.docker_helpers.image_finder import ImageFinder

class ContainerFinder:
	docker = None

	def __init__(self, docker):
		self.docker = docker
		self.imageFinder = ImageFinder(docker)

	def expectedLabel(self):
		return 'envy-' + appConfig.getConfigFileHash() + '-container'

	def findAndEnsureRunning(self):
		# List only running containers
		container = self.findContainer()
		if 'running' not in container.status:
			container.start()
		return container

	def findContainer(self):
		expectedLabel = self.expectedLabel()
		containers = self.docker.containers.list(all=True)
		for container in containers:
			if container.name == expectedLabel:
				return container
		imageId = self.imageFinder.findImage()
		logging.info('Creating new container for: %s', imageId)
		container = self.docker.containers.create(imageId, 'tail -f /dev/null', name=expectedLabel)
		return container
