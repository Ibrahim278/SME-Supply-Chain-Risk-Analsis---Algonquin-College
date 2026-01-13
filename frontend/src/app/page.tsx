import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';

export default function Home() {
  return (
    <main className="min-h-screen bg-neutral-50">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-neutral-900 mb-4">
            SME Supply Chain Risk Analysis
          </h1>
          <p className="text-lg md:text-xl text-neutral-600 max-w-2xl mx-auto mb-8">
            AI-powered supply chain risk assessment for SME suppliers. Identify
            risks, validate compliance, and secure your supply chain.
          </p>
          <div className="flex gap-4 justify-center flex-col sm:flex-row">
            <Button size="lg" className="bg-primary hover:bg-primary-dark">
              Get Started
            </Button>
            <Button size="lg" variant="outline">
              Learn More
            </Button>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          <Card className="border-neutral-200">
            <CardHeader>
              <CardTitle className="text-primary">Risk Assessment</CardTitle>
              <CardDescription>
                Comprehensive AI-driven analysis of supplier risk factors
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-neutral-600 text-sm">
                Automated evaluation of compliance status, and operational risks
                across your supply chain.
              </p>
            </CardContent>
          </Card>

          <Card className="border-neutral-200">
            <CardHeader>
              <CardTitle className="text-primary">
                Evidence Collection
              </CardTitle>
              <CardDescription>
                Automated data gathering from multiple sources
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-neutral-600 text-sm">
                Collects and analyzes data from public records, regulatory
                databases, and supplier documentation.
              </p>
            </CardContent>
          </Card>

          <Card className="border-neutral-200">
            <CardHeader>
              <CardTitle className="text-primary">Detailed Reports</CardTitle>
              <CardDescription>
                Actionable insights and recommendations
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-neutral-600 text-sm">
                Generate comprehensive reports with risk scores, findings, and
                recommended follow-up actions.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Status Indicators */}
        <div className="mt-16 text-center">
          <div className="inline-flex gap-6 flex-wrap justify-center">
            <span className="inline-flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-success"></span>
              <span className="text-sm text-neutral-600">Low Risk</span>
            </span>
            <span className="inline-flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-warning"></span>
              <span className="text-sm text-neutral-600">Medium Risk</span>
            </span>
            <span className="inline-flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-error"></span>
              <span className="text-sm text-neutral-600">High Risk</span>
            </span>
          </div>
        </div>
      </div>
    </main>
  );
}
