from dataclasses import dataclass, field


@dataclass
class EntityMetadata:

    name: str

    fields: list = field(default_factory=list)

    relations: list = field(default_factory=list)

    permissions: list = field(default_factory=list)

    workflows: list = field(default_factory=list)



class EnterpriseMetadataGenerator:


    def generate(self, blueprint):

        entities = []


        for module in blueprint.modules:

            entity = EntityMetadata(
                name=module
            )


            entity.fields = [
                "id",
                "name",
                "created_at",
                "updated_at"
            ]


            entity.relations = []


            entity.permissions = [
                "create",
                "read",
                "update",
                "delete"
            ]


            entity.workflows = [
                "approval",
                "validation"
            ]


            entities.append(
                entity
            )


        return {
            "entities": entities,
            "count": len(entities),
            "multi_tenant": True
        }
