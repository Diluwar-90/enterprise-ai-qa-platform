from app.services.azure_search_index import AzureSearchIndexService


def main() -> None:
    service = AzureSearchIndexService()
    index = service.create_index()

    print(f"Created Azure AI Search index: {index.name}")


if __name__ == "__main__":
    main()