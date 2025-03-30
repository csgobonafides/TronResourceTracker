from fastapi import APIRouter, Depends, status
import logging

from controller.tron_control import get_controller, TronController
from schemas.tron import TronDtlInfo, TronFullInfo


router = APIRouter()
logger =logging.getLogger('tron_api')


@router.post('/', response_model=TronDtlInfo, status_code=status.HTTP_201_CREATED)
async def account_resource(
        address: str,
        controller: TronController = Depends(get_controller)
) -> TronDtlInfo:
    return await controller.add_resource(address=address)


@router.get('/', response_model=list[TronFullInfo], status_code=status.HTTP_200_OK)
async def account_requests_list(
        page: int = 1,
        page_size: int = 5,
        controller: TronController = Depends(get_controller)
) -> list[TronFullInfo]:
    return await controller.get_resource(page=page, page_size=page_size)
