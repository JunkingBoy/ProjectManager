from typing import Optional
from fastapi import Request


async def yield_dashboard_service(
    r: Request,
    year: Optional[int] = None,
    system: Optional[str] = None,
    project_type: Optional[str] = None,
) -> dict:
    return {
        "total_received": 120,
        "total_amount": 84000,
        "not_started": 10,
        "completed": 85,
        "in_development": 15,
        "in_testing": 10,
        "monthly_received": [
            {"month": "1月", "count": 12, "amount": 8400},
            {"month": "2月", "count": 20, "amount": 14000},
            {"month": "3月", "count": 15, "amount": 10500},
            {"month": "4月", "count": 8, "amount": 5600},
            {"month": "5月", "count": 22, "amount": 15400},
            {"month": "6月", "count": 18, "amount": 12600},
        ],
        "monthly_completed": [
            {"month": "1月", "count": 10, "amount": 7000},
            {"month": "2月", "count": 18, "amount": 12600},
            {"month": "3月", "count": 14, "amount": 9800},
            {"month": "4月", "count": 7, "amount": 4900},
            {"month": "5月", "count": 20, "amount": 14000},
            {"month": "6月", "count": 16, "amount": 11200},
        ],
    }


async def employee_dashboard_service(
    r: Request,
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> dict:
    return {
        "in_progress": [
            {"name": "张三", "score": 9.5},
            {"name": "李四", "score": 11.5},
            {"name": "王五", "score": 8.0},
            {"name": "赵六", "score": 16.4},
        ],
        "delayed": [
            {"name": "张三", "score": 2.0},
            {"name": "李四", "score": 0},
            {"name": "王五", "score": 1.5},
            {"name": "赵六", "score": 0},
        ],
        "performance": [
            {"name": "张三", "score": 15.0},
            {"name": "李四", "score": 20.0},
            {"name": "王五", "score": 18.0},
            {"name": "赵六", "score": 22.0},
        ],
    }
