import React from "react";
import {
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  Paging,
  Facet
} from "@elastic/search-ui";
import { ElasticSearchConnector } from "@elastic/search-ui-elasticsearch-connector";

const connector = new ElasticSearchConnector({
  host: "http://localhost:9200",
  index: "cv-transcriptions"
});

const config = {
  apiConnector: connector,
  searchQuery: {
    search_fields: {
      generated_text: {},
      age: {},
      gender: {},
      duration: {},
      accent: {}
    },
    result_fields: {
      generated_text: { raw: {} },
      age: { raw: {} },
      gender: { raw: {} },
      duration: { raw: {} },
      accent: { raw: {} }
    },
    facets: {
      gender: { type: "value" },
      accent: { type: "value" },
      age: { type: "value" }
    }
  }
};

function App() {
  return (
    <SearchProvider config={config}>
      <div className="App">
        <SearchBox />
        <Facet field="gender" />
        <Facet field="accent" />
        <Facet field="age" />
        <PagingInfo />
        <Results
          titleField="generated_text"
          urlField="duration"
        />
        <Paging />
      </div>
    </SearchProvider>
  );
}

export default App;
