module Jekyll
  class TwemojiAwesomeTag < Liquid::Tag

    def render(context)
      if tag_contents = determine_arguments(@markup.strip)
        twa_class, twa_extra = tag_contents[0], tag_contents[1]
        twa_tag(twa_class, twa_extra)
      else
        raise ArgumentError.new <<-eos
Syntax error in tag 'twa' while parsing the following markup:

  #{@markup}

Valid syntax:
  for twas: <i class="twa twa-heart"></i>
eos
      end
    end

    private

    def determine_arguments(input)
      matched = input.match(/\A(\S+) ?(\S+)?\Z/)
      [matched[1].to_s.strip, matched[2].to_s.strip] if matched && matched.length >= 3
    end

    def twa_tag(twa_class, twa_extra = nil)
      if twa_extra.empty?
        "<i class=\"twa #{twa_class}\"></i>"
      else
        "<i class=\"twa #{twa_class} #{twa_extra}\"></i>"
      end
    end
  end
end

Liquid::Template.register_tag('twa', Jekyll::TwemojiAwesomeTag)
