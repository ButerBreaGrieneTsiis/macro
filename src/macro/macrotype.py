from typing import Any, Dict


class MacroType:
    
    @classmethod
    def van_json(
        cls,
        **dict,
        ) -> "MacroType":
        
        return cls(**dict)
    
    def naar_json(self) -> Dict[str, Any]:
        ...