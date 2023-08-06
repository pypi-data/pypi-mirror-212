from __future__ import annotations

import python_graphql_client
import logging
from typing import Dict, List
from sumatra_client.auth import CognitoJwtAuth
from sumatra_client.config import CONFIG

logger = logging.getLogger("sumatra.cli")


class AdminClient:
    """
    Admin Client to connect to Sumatra GraphQL API as an instance administrator.
    Not creatable if you are not logged in as an admin user.

    __Humans:__ First, log in via the CLI: `sumatra login`
    """

    def __init__(self):
        self._gql_client = python_graphql_client.GraphqlClient(
            auth=CognitoJwtAuth("_new"), endpoint=CONFIG.console_graphql_url
        )
        if not self._is_admin():
            raise ValueError(
                "Unable to create an AdminClient when not logged in as an instance admin."
            )

    def _is_admin(self) -> bool:
        logger.debug("Fetching currentUser")
        query = """
        query CurrentUser {
            currentUser {
                admin
            }
        }
        """

        ret = self._gql_client.execute(query=query)

        if "errors" in ret:
            raise RuntimeError(ret["errors"][0]["message"])

        return ret["data"]["currentUser"]["admin"]

    def upgrade_tenant(self, tenant: str) -> None:
        """
        Upgrade tenant to paid tier.

        Arguments:
            tenant: The slug of the tenant to upgrade.
        """
        query = """
            mutation UpgradeTenant($id: String!) {
                upgradeTenant(id: $id) {
                    id
                }
            }
        """

        ret = self._gql_client.execute(
            query=query,
            variables={"id": self._tenant_id_from_slug(tenant)},
            headers={"x-sumatra-tenant": tenant},
        )

        if "errors" in ret:
            raise RuntimeError(ret["errors"][0]["message"])

    def downgrade_tenant(self, tenant: str) -> None:
        """
        Downgrade tenant to free tier.

        Arguments:
            tenant: The slug of the tenant to downgrade.
        """
        query = """
            mutation DowngradeTenant($id: String!) {
                downgradeTenant(id: $id) {
                    id
                }
            }
        """

        ret = self._gql_client.execute(
            query=query,
            variables={"id": self._tenant_id_from_slug(tenant)},
            headers={"x-sumatra-tenant": tenant},
        )

        if "errors" in ret:
            raise RuntimeError(ret["errors"][0]["message"])

    def set_quota(self, tenant: str, monthly_events: int) -> None:
        """
        Set quota for tenant.
        """
        query = """
            mutation SetQuota($id: String!, $monthlyEvents: Int!) {
                updateTenant(id: $id, monthlyEvents: $monthlyEvents) {
                    id
                }
            }
        """
        ret = self._gql_client.execute(
            query=query,
            variables={
                "id": self._tenant_id_from_slug(tenant),
                "monthlyEvents": monthly_events,
            },
            headers={"x-sumatra-tenant": tenant},
        )

        if "errors" in ret:
            raise RuntimeError(ret["errors"][0]["message"])

    def list_users(self) -> List[str]:
        """
        List all users on instance.
        """
        query = """
            query ListUsers {
                users(first: 60) {
                    nodes {
                        username
                    }
                }
            }
        """

        ret = self._gql_client.execute(query=query)

        if "errors" in ret:
            raise RuntimeError(ret["errors"][0]["message"])

        return [user["username"] for user in ret["data"]["users"]["nodes"]]

    def get_user(self, username: str) -> Dict[str, str]:
        """
        Get metadata for user.
        """
        query = """
            query User($username: String!) {
                user(username: $username) {
                    username
                    email
                    admin
                    status
                    sso
                }
            }
        """

        ret = self._gql_client.execute(
            query=query,
            variables={
                "username": username,
            },
        )

        if "errors" in ret:
            raise RuntimeError(ret["errors"][0]["message"])

        return ret["data"]["user"]

    def _tenant_id_from_slug(self, slug: str) -> str:
        query = """
            query TenantIDFromSlug($slug: String!) {
                tenantIdFromSlug(slug: $slug)
            }
        """

        ret = self._gql_client.execute(
            query=query,
            variables={
                "slug": slug,
            },
        )

        if "errors" in ret:
            raise RuntimeError(ret["errors"][0]["message"])

        id = ret["data"]["tenantIdFromSlug"]
        if not id:
            raise ValueError(f"Unknown slug {slug}")
        return id

    def list_tenants(self) -> None:
        """
        List all tenants on instance.
        """
        query = """
                query ListTenants {
                    tenants {
                        nodes {
                            key
                        }
                    }
                }
            """

        ret = self._gql_client.execute(query=query)

        if "errors" in ret:
            raise RuntimeError(ret["errors"][0]["message"])

        return [tenant["key"] for tenant in ret["data"]["tenants"]["nodes"]]
