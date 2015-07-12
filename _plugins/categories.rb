#
# Plugin to generate an index page for every category
#

module Jekyll

  class CategoryPage < Page
    def initialize(site, base, category)
      @site = site
      @base = base
      @dir = category
      @name = 'index.html'

      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'category_index.html')
      self.data['category'] = category

      category_title_prefix = site.config['category_title_prefix'] || 'Category: '
      self.data['categories'] = "exclude"           # don't create a link in the site header
      self.data['title'] = "#{category_title_prefix}#{category}"
    end
  end

  class CategoryPageGenerator < Generator
    safe true

    def generate(site)
      if site.layouts.key? 'category_index'
        site.categories.each_key do |category|
          site.pages << CategoryPage.new(site, site.source, category)
        end
      end
    end
  end

end
