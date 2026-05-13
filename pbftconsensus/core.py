from dataclasses import dataclass, field

@dataclass
class Replica:
    id: int
    log: list[str] = field(default_factory=list)

class PBFTCluster:
    def __init__(self, n: int, f: int | None = None) -> None:
        assert n >= 3
        self.n = n
        self.f = f if f is not None else (n - 1) // 3
        self.replicas = [Replica(i) for i in range(n)]
        self.primary = 0

    def _quorum(self) -> int:
        return 2 * self.f + 1

    def commit_request(self, value: str) -> bool:
        # pre-prepare from primary
        prepares = 1
        commits = 0
        for r in self.replicas:
            if r.id == self.primary:
                r.log.append(f"preprepare:{value}")
            else:
                r.log.append(f"prepare:{value}")
            prepares += 1
        if prepares < self._quorum():
            return False
        for r in self.replicas:
            r.log.append(f"commit:{value}")
            commits += 1
        return commits >= self._quorum()

    def agreed_values(self) -> list[str]:
        out = []
        for r in self.replicas:
            for entry in r.log:
                if entry.startswith("commit:"):
                    val = entry.split(":", 1)[1]
                    if val not in out:
                        out.append(val)
        return out
