from pbftconsensus.core import PBFTCluster

def test_commit_success():
    c = PBFTCluster(4)
    assert c.commit_request("tx1") is True

def test_all_replicas_log():
    c = PBFTCluster(4)
    c.commit_request("a")
    assert all("commit:a" in r.log for r in c.replicas)

def test_quorum_three():
    assert PBFTCluster(4)._quorum() == 3

def test_agreed_values():
    c = PBFTCluster(4)
    c.commit_request("z")
    assert "z" in c.agreed_values()

def test_primary_id():
    assert PBFTCluster(7).primary == 0
