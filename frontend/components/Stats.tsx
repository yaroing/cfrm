const stats = [
  { name: 'Organisations partenaires', value: '50+' },
  { name: 'Pays couverts', value: '25+' },
  { name: 'Langues supportées', value: '15+' },
  { name: 'Tickets traités/mois', value: '10K+' },
]

export default function Stats() {
  return (
    <div className="bg-primary-600">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:py-16 sm:px-6 lg:px-8 lg:py-20">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-extrabold text-white sm:text-4xl">
            Confiance des organisations humanitaires
          </h2>
          <p className="mt-3 text-xl text-primary-200 sm:mt-4">
            Une plateforme éprouvée dans le secteur humanitaire
          </p>
        </div>
        <dl className="mt-10 max-w-md mx-auto grid grid-cols-1 gap-8 sm:max-w-2xl sm:grid-cols-2 lg:max-w-4xl lg:grid-cols-4">
          {stats.map((stat) => (
            <div key={stat.name} className="flex flex-col">
              <dt className="order-2 mt-2 text-lg leading-6 font-medium text-primary-200">
                {stat.name}
              </dt>
              <dd className="order-1 text-5xl font-extrabold text-white">
                {stat.value}
              </dd>
            </div>
          ))}
        </dl>
      </div>
    </div>
  )
}
