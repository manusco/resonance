// Representative implementation for workspace record inspection.
export function CustomersDetail({ customer }) {
  return <ContextualDrawer record={customer} onClose="restore-table-context" />;
}
