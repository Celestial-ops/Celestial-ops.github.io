// This snippet gets injected into the 'Update' method of the player controller
GameObject[] enemies = GameObject.FindGameObjectsWithTag("Player");
foreach (GameObject enemy in enemies) {
    if (enemy != this.gameObject) {
        LineRenderer line = enemy.GetComponent<LineRenderer>();
        if (line == null) {
            line = enemy.AddComponent<LineRenderer>();
            line.material = new Material(Shader.Find("Hidden/Internal-Colored"));
            line.startWidth = 0.01f;
            line.endWidth = 0.01f;
        }
        line.SetPosition(0, transform.position); // Start at your VR position
        line.SetPosition(1, enemy.transform.position); // End at target position
    }
}
