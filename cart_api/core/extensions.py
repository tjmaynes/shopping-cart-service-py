from typing import List, TypeVar
import python_either.either as E


T = TypeVar("T")
U = TypeVar("U")


def convert_list_to_either(items: List[E.Either[T, Exception]]) -> E.Either[List[U], Exception]:
    success_results = []
    
    for item in items:
        success_result, failure_result = item | E.from_either | dict(
            if_success=(lambda result: (result, None)),
            if_failure=(lambda ex: (None, ex))
        )

        if success_result is not None:
            success_results.append(success_result)
        elif failure_result is not None:
            return E.failure(failure_result)
        else:
            return E.failure(Exception("Unexpected error has occurred!"))
    return E.success(success_results)