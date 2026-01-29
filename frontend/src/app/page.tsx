export default function Home() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-6">
        Welcome to ScholarPASS Sales Campaign
      </h1>
      <div className="bg-white rounded-lg shadow-md p-6">
        <p className="text-gray-600 mb-4">
          Manage your opportunities and campaigns efficiently.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold text-gray-700 mb-2">
              Opportunity Pipelines
            </h2>
            <p className="text-gray-600 text-sm">
              Track and manage your sales opportunities through different pipeline stages.
            </p>
          </div>
          <div className="border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold text-gray-700 mb-2">
              Campaigns
            </h2>
            <p className="text-gray-600 text-sm">
              Create and monitor marketing campaigns to drive sales growth.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
