def test_health(client):
    assert client.get("/health").json()=={"status":"ok"}

def test_submit_and_fetch(client):
    r=client.post("/jobs",json={"name":"api-test","duration_s":0.1})
    assert r.status_code==201
    assert client.get("/jobs/"+r.json()["id"]).status_code==200

def test_cpu_over_capacity_rejected(client):
    assert client.post("/jobs",json={"name":"oversized","cpu":99}).status_code==422

def test_invalid_payload_rejected(client):
    assert client.post("/jobs",json={"name":"","cpu":0}).status_code==422

def test_unknown_job_returns_404(client):
    assert client.get("/jobs/missing-id").status_code==404

def test_invalid_status_filter(client):
    assert client.get("/jobs?status=not-valid").status_code==400

def test_cluster_shape(client):
    data=client.get("/cluster").json()
    assert data["workers"]==2 and data["cpu_capacity"]==4
