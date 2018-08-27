import com.cloudbees.opscenter.server.model.ClientMaster
import com.cloudbees.opscenter.server.model.OperationsCenter


def clientMasterName = "{{ name }}"
ClientMaster clientMaster = OperationsCenter.instance.createClientMaster(clientMasterName)

if (OperationsCenter.instance.getConnectedMasterByName(clientMaster.idName)!=null){
    println "Created ClientMaster '${clientMaster.name}' known as '${clientMaster.idName}'"
    println "-DMASTER_INDEX=${clientMaster.id}'"
    println "-DMASTER_NAME=${clientMaster.name}'"
    println "-DMASTER_GRANT_ID=${clientMaster.grantId}'"
} else {
    println "[ERROR:]" + clientMasterName + "has not been created in CJOC"
}
