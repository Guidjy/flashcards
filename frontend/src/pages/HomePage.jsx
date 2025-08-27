import MainLayout from "../layouts/MainLayout"
// components
import Table from "../components/Table"


export default function HomePage() {
  return (
    <>
      <MainLayout>
        <Table
          columns={["Name", "Cards", "Edit"]}
          rows={[{"name": "deck 1", "cardCount": 10}, {"name": "deck 2", "cardCount": 30}]}
        />
      </MainLayout>
    </>
  )
}