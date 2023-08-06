from typing import Union
from cqlpy._internal.exceptions import ValueSetProviderError
from cqlpy._internal.types.value_set import ValueSet
from cqlpy._internal.types.value_set_scope import ValueSetScope
from cqlpy._internal.valueset_provider import ValueSetProvider, ValueSetScopeProvider


class CqlValueSetProvider:
    def __init__(self, valueset_provider: ValueSetProvider) -> None:
        self._valueset_provider = valueset_provider

    def __get_valueset(self, item: ValueSet) -> ValueSet:
        if item.id is None:
            raise ValueError("value set id must be specified")

        name = item.id.replace("http://cts.nlm.nih.gov/fhir/ValueSet/", "")
        result = self._valueset_provider.get_valueset(name=name, scope=None)

        if result:
            return ValueSet.parse_fhir_json(result)

        print(f"value set 'scopeless:{item.name}' not found")

        return item

    def __get_valueset_scope(self, item: ValueSetScope) -> list[ValueSet]:
        if not isinstance(self._valueset_provider, ValueSetScopeProvider):
            raise ValueSetProviderError(
                "The value set provider does not support scope-based value set retrieval"
            )

        if item.id is None:
            raise ValueError("value set scope id must be specified")

        result = self._valueset_provider.get_valuesets_in_scope(scope=item.id)

        if result:
            return [ValueSet.parse_fhir_json(value_set) for value_set in result]

        print(f"value set scope '{item.id}' not found")

        return []

    def __getitem__(
        self, item: Union[ValueSet, ValueSetScope]
    ) -> Union[ValueSet, list[ValueSet]]:
        if isinstance(item, ValueSetScope):
            return self.__get_valueset_scope(item)
        return self.__get_valueset(item)
