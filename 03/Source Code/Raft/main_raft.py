import time
from raft_module import RaftNode, State


def simulate_raft():
    node_ids = [1, 2, 3]
    nodes = [RaftNode(i, node_ids) for i in node_ids]

    print("Simulasi Raft menggunakan modul Python")
    print("Jumlah node:", len(nodes))

    # Simulasikan pemilihan pemimpin
    nodes[0].start_election()

    # Simulasi beberapa langkah
    for step in range(20):
        time.sleep(0.5)
        print(f"\n--- Step {step + 1} ---")

        leaders = [
            node for node in nodes
            if node.state == State.LEADER
        ]

        if leaders:
            leader = leaders[0]

            # Kirim heartbeat kepada follower
            for node in nodes:
                if node.id != leader.id:
                    node.on_heartbeat(leader.current_term)

            # Leader menambahkan perintah
            if step % 2 == 0:
                leader.append_entry(f"command-{step}")

        # Tampilkan status setiap node
        for node in nodes:
            print(
                f"Node {node.id}: {node.state.name} | "
                f"Term {node.current_term} | "
                f"Log len {len(node.log)}"
            )


if __name__ == "__main__":
    simulate_raft()
