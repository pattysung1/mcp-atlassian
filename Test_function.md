# Confluence Tools Test Checklist

This document summarizes the test cases for the `mcp-atlassian` Confluence tools and their current status based on our debugging session.

---

## Test Checklist

### 1. Get Page Information
- [x] **Get a page by its title to find its ID.**
  - ✅ **Successful Prompt:**
    ```
    In the CJT space, what is the page ID for the page named "[TEST] MCP Confluence Integration"?
    ```

### 2. Create a Page
- [x] **Create a simple page with title and content.**
  - ✅ **Successful Prompt:**
    ```
    Create a new page in the CJT space with the title "Test 9/18" with the content "This is a test page created by the agent to verify access."
    ```
- [x] **Create a child page under a parent page.**
  - 📝 **Note:** This is a two-step process. You must first get the `parent_id` and then use it to create the child page.
  - ✅ **Successful Prompt (Step 1 - Get ID):**
    ```
    In the CJT space, what is the page ID for the page named "[TEST] MCP Confluence Integration"?
    ```
  - ✅ **Successful Prompt (Step 2 - Create with ID):**
    ```
    Create a new page in the CJT space with the title "Test 9/18 - Child Page" with the content "This is a child page" and a parent_id of 1022021709.
    ```

### 3. Update Page
- [x] **Update a page's title and content.**
  - 📝 **Note:** The `update_page` tool requires `page_id`, `title`, and `content` to be provided in every call, even if you only intend to change one of them. You must provide the full desired content of the page.
  - ✅ **Successful Prompt:**
    ```
    Update the page with ID 1022021709. Set the new title to "[TEST][UPDATED] MCP Confluence Integration" and use the following as the full content:
    "# MCP Test Page

    This is a test page created for verifying MCP and Confluence API integration.

    ## Test Information
    - Project Name: MCP test
    - Test ID: TST-001
    - Owner: Patty Sung
    - Test Status: In Progress
    - Last Updated: 2025-09-18

    ## Test Checklist
    - [ ] Create a page
    - [ ] Update page content
    - [ ] Retrieve page information
    - [ ] Add a child page
    - [ ] Delete the page"
    ```

### 4. Add Labels
- [x] **Add a single label to a page.**
  - 📝 **Note:** The `add_label` tool can only add one label at a time. To add multiple labels, you must issue multiple separate commands.
  - ✅ **Successful Prompt:**
    ```
    Add the label 'single-test' to the page with ID 1022021709.
    ```

### 5. Delete Page
- [x] **Delete a page by its ID.**
  - 📝 **Note:** The agent may fail to find the page ID automatically from a title. The most reliable method is a two-step process: first find the ID, then command the deletion using the ID.
  - ✅ **Successful Prompt (Step 1 - Get ID):**
    ```
    In the CJT space, what is the page ID for the page titled 'Test for delete'?
    ```
  - ✅ **Successful Prompt (Step 2 - Delete with ID):**
    ```
    Delete the page with ID 1022024137.
    ```