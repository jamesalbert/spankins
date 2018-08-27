def instance=jenkins.model.Jenkins.instance
instance.setSlaveAgentPort({{ port }})
instance.save()
